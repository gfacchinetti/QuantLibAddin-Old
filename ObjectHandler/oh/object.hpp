
/*
 Copyright (C) 2004, 2005 Eric Ehlers

 This file is part of QuantLib, a free-software/open-source library
 for financial quantitative analysts and developers - http://quantlib.org/

 QuantLib is free software: you can redistribute it and/or modify it under the
 terms of the QuantLib license.  You should have received a copy of the
 license along with this program; if not, please email quantlib-dev@lists.sf.net
 The license is also available online at http://quantlib.org/html/license.html

 This program is distributed in the hope that it will be useful, but WITHOUT
 ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
 FOR A PARTICULAR PURPOSE.  See the license for more details.
*/

/*! \file
    \brief Object class
*/

#ifndef oh_object_hpp
#define oh_object_hpp

#include <boost/shared_ptr.hpp>
#include <boost/any.hpp>
#include <oh/property.hpp>
#include <oh/valueobject.hpp>
#include <vector>
#include <stack>
#include <string>
#include <iostream>

/* Use BOOST_MSVC instead of _MSC_VER since some other vendors 
   (Metrowerks, for example) also #define _MSC_VER
*/
#if defined BOOST_MSVC       // Microsoft Visual C++
#pragma warning(disable:4231)
#endif

namespace ObjHandler {
    //! Shared pointer to any.
    /*! Used to hold the value for
        each of the Object's properties.
    */
    typedef boost::shared_ptr<boost::any> any_ptr;
    //! Property string/any pair.
    /*! The string names the property
        and the any holds the corresponding value.
    */
    //typedef Property<std::string, any_ptr> ObjectProperty;
    //! Property vector.
    /*! Each Object is described by a vector of properties
        which is maintained dynamically throughout
        the life of the Object.
    */
    //typedef std::vector<ObjectProperty> Properties;

    //! ABC implementing interface for Objects to be stored in the ObjectHandler.
    /*! Objects are constructed via the Factory function makeObject
        and stored in the global ObjectHandler repository.
    */
    class Object {        
    public:
        //! \name Constructors & Destructors
        //@{
        //! Default constructor.
        /*! Construct an Object.
            To store the resulting Object in the ObjectHandler, call
                ObjectHandler::instance().storeObject(handle, object);
        */
        Object() {};
        //! Default destructor.
        virtual ~Object() {};
        //@}
        //! \name Object interrogation
        //@{
        //! Acquire a reference to underlying Object.
        /*! Returns a reference to the client object stored in the Object.
            This is a shared pointer to void which must be recast appropriately.
        */
        virtual boost::shared_ptr<void> getReference() const = 0;
        //! Return the Object's property vector.
        /*! Returns the property vector describing the underlying Object.
        */
        //const Properties& getProperties() const;
        //! Retrieve vector of property names.
        /*! Returns empty vector if Object has no properties.
        */
        const std::vector < std::string > propertyNames() const;
        //! Retrieve value of given property.
        /*! Throws exception if Object has no property by that name.
        */
        const boost::any propertyValue(const std::string &propertyName) const;

        friend std::ostream &operator<<(std::ostream&, const Object &object);
        //@}
        void setProperties(const boost::shared_ptr<ValueObject>& p) {
            mProps = p;
        }

    protected:
        /*template < class T >
        void createProperty(const std::string &name, const T &value) {
            any_ptr anyValue(new boost::any(value));
            ObjectProperty objectProperty(name, anyValue);
            properties_.push_back(objectProperty);
        }

        template < class T >
        void updateProperty(const int &index, const T &value) {
            *properties_[index]() = value;
        }*/

    private:
        boost::shared_ptr<ValueObject> mProps;
        //Properties properties_;
        Object& operator= (const Object&);
        Object(const Object&);
    };

    /*! \relates Object */
    //! any_ptr ostream operator.
    /*! Write contents of boost::any to output stream.
    */
    std::ostream& operator<<(std::ostream& out, const boost::any& any);

    /*! \relates Object */
    //! obj_ptr ostream operator.
    /*! Write contents of Object Property vector to output stream.
    */

    std::ostream& operator<<(std::ostream& out, const Object &object);

    template < typename T >
    std::ostream& operator<<(std::ostream& out, std::vector < T > &v) {
        out << std::endl;
        for (typename std::vector< T >::const_iterator i = v.begin(); i != v.end(); i++)
            out << *i << std::endl;
        return out;
    }

}

#endif

